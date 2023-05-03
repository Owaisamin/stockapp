from rest_framework import serializers
from stocks.models import *
from django.utils.translation import ugettext_lazy as _

class LoginSerializer(serializers.Serializer):
    """User login serializer
    """
    email = serializers.EmailField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, instance):
        if len(instance["password"]) < 8:
            raise serializers.ValidationError(_("Password must be at least 8 characters long."))

        return instance

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = "__all__"

    # def to_representation(self, instance):
    #     data = super(CitySerializer, self).to_representation(instance)
    #     data['region'] = RegionSerializer(instance.region).data
    #     return data
