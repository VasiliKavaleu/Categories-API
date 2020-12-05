import itertools

from rest_framework import serializers

from .models import Category


class AllChildrenField(serializers.RelatedField):
    """ Overriding deserialization behavior. """

    def to_internal_value(self, data):
        result = []
        stack = [data]

        while stack:
            category = stack.pop()
            name = category.get('name')
            if not name:
                raise ValueError("name field is required.")

            for child in reversed(category.get('children', [])):
                child['parent'] = name
                stack.append(child)

            result.append({'name': name, 'parent': category.get('parent', None)})

        return result


class BaseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):

    children = AllChildrenField(many=True, queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ['name', 'children']

    def create(self, validated_data):
        validated_data['children'] = list(itertools.chain.from_iterable(validated_data.get('children', [])))
        category = Category(name=validated_data.get('name'))
        category.save()
        categories = {category.name: category}

        for child in validated_data.get('children'):
            child_category = Category(name=child.get('name'), parent=categories.get(child.get('parent'))) \
                if child.get('parent') else Category(name=child.get('name'), parent=category)

            child_category.save()
            categories[child_category.name] = child_category

        return category


class CategoriesSerializer(serializers.ModelSerializer):
    """ Serialization data with added info(parents, children, siblings) by calling a methods. """

    parents = serializers.SerializerMethodField(method_name="get_parents")
    children = serializers.SerializerMethodField(method_name="get_children")
    siblings = serializers.SerializerMethodField(method_name="get_siblings")

    class Meta:
        model = Category
        fields = ['id', 'name', 'parents', 'children', 'siblings']

    def get_parents(self, obj):
        serializer = BaseCategorySerializer(instance=self.get_parents_tree(obj), many=True)
        return serializer.data

    def get_children(self, obj):
        serializer = BaseCategorySerializer(instance=obj.children.all(), many=True)
        return serializer.data

    def get_siblings(self, obj):
        serializer = BaseCategorySerializer(instance=Category.objects.filter(parent=obj.parent).exclude(pk=obj.pk), many=True)
        return serializer.data

    def get_parents_tree(self, obj):
        categories = []
        category = obj.parent
        while category is not None:
            categories.append(category)
            category = category.parent

        return categories