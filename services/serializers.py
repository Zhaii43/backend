from rest_framework import serializers
from .models import Service, ServiceImage, Booking, WorkSpecification, Review, Reply

class WorkSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpecification
        fields = ['id', 'name', 'price']

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id', 'image']

class ReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())

    class Meta:
        model = Reply
        fields = ['id', 'user', 'review', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None
        if not user.is_authenticated:
            raise serializers.ValidationError("You must be logged in to reply.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    replies = ReplySerializer(many=True, read_only=True)
    rating_label = serializers.ChoiceField(choices=Review.RATING_LABEL_CHOICES)

    class Meta:
        model = Review
        fields = ['id', 'user', 'service', 'rating', 'rating_label', 'comment', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at', 'replies']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    work_specifications = WorkSpecificationSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'category', 'title', 'description', 'location', 'images', 'work_specifications', 'reviews']

class BookingServiceSerializer(serializers.ModelSerializer):
    images = ServiceImageSerializer(many=True, read_only=True)
    work_specifications = WorkSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'title', 'location', 'images', 'work_specifications']

class BookingSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), allow_null=True)
    service_detail = BookingServiceSerializer(source='service', read_only=True)
    work_specifications = serializers.PrimaryKeyRelatedField(
        queryset=WorkSpecification.objects.all(), many=True, write_only=True, required=False
    )
    work_specifications_detail = WorkSpecificationSerializer(source='work_specifications', many=True, read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    address = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'service', 'service_detail', 'work_specifications', 'work_specifications_detail', 'price', 'booking_date', 'booking_time', 'address', 'latitude', 'longitude', 'is_editable', 'status', 'created_at']
        read_only_fields = ['user', 'is_editable', 'status', 'created_at', 'service_detail', 'work_specifications_detail']

    def validate_service(self, value):
        if value and not Service.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(f"Service with ID {value.id} does not exist.")
        return value

    def validate_work_specifications(self, value):
        if not value:
            return value
        for spec in value:
            if not WorkSpecification.objects.filter(id=spec.id).exists():
                raise serializers.ValidationError(f"Work specification with ID {spec.id} does not exist.")
        return value

    def validate_address(self, value):
        if value and not value.strip():
            raise serializers.ValidationError("Address cannot be empty.")
        return value

    def validate(self, data):
        booking_date = data.get('booking_date')
        booking_time = data.get('booking_time')
        service = data.get('service')
        work_specifications = data.get('work_specifications', [])
        price = data.get('price')
        address = data.get('address')
        user = self.context['request'].user  # Get the current user

        if self.instance:  # Update case
            booking_date = booking_date or self.instance.booking_date
            booking_time = booking_time or self.instance.booking_time
            service = service or self.instance.service
            work_specifications = work_specifications or list(self.instance.work_specifications.all())
            price = price or self.instance.price
            address = address or self.instance.address

        # Check for existing booking for the same user, service, date, and time
        if service and booking_date and booking_time:
            existing_booking = Booking.objects.filter(
                user=user,
                service=service,
                booking_date=booking_date,
                booking_time=booking_time
            ).exclude(id=self.instance.id if self.instance else None)
            if existing_booking.exists():
                raise serializers.ValidationError(
                    f"You already have a booking for this service on {booking_date} at {booking_time}. Please choose a different time or date."
                )

        if work_specifications and service:
            for spec in work_specifications:
                if spec.service != service:
                    raise serializers.ValidationError(
                        f"The work specification '{spec.name}' does not belong to the chosen service."
                    )

        if price is not None and price < 0:
            raise serializers.ValidationError("A valid total price in Philippine Peso is required.")

        if work_specifications:
            expected_price = sum(spec.price for spec in work_specifications)
            if price is not None and price != expected_price:
                raise serializers.ValidationError(
                    f"The provided total price (PHP {price}) does not match the sum of work specification prices (PHP {expected_price})."
                )

        return data

    def update(self, instance, validated_data):
        work_specifications = validated_data.pop('work_specifications', None)
        instance = super().update(instance, validated_data)
        if work_specifications is not None:
            instance.work_specifications.set(work_specifications)
        return instance