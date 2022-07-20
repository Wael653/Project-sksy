from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nummer', models.CharField(max_length=15, verbose_name='Nummer')),
            ],
        ),
        migrations.CreateModel(
            name='RoomDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(max_length=160, verbose_name='Bezeichnung')),
                ('anzahl', models.PositiveIntegerField(default=1, verbose_name='Anzahl')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('straße', models.CharField(default='Straße des 17. Juni', max_length=50, verbose_name='Straße')),
                ('hausnummer', models.CharField(default='135', max_length=10, verbose_name='Hausnummer')),
                ('postleitzahl', models.CharField(default='10623', max_length=5, verbose_name='Postleitzahl')),
                ('etage', models.IntegerField(default=0, verbose_name='Etage')),
            ],
        ),
        migrations.CreateModel(
            name='WorkplaceDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(max_length=160, verbose_name='Bezeichnung')),
                ('anzahl', models.PositiveIntegerField(default=1, verbose_name='Anzahl')),
            ],
        ),
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nummer', models.PositiveIntegerField()),
                ('anzahlPersonen', models.PositiveIntegerField(default=1)),
                ('sonstiges', models.CharField(blank=True, max_length=160, null=True)),
                ('barrierefrei', models.BooleanField(blank=True, default=True, null=True, verbose_name='Barrierefrei')),
                ('geraete', models.ManyToManyField(blank=True, to='starsApp.workplacedevice')),
                ('raum', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='starsApp.room')),
            ],
            options={
                'ordering': ['nummer'],
            },
        ),
        migrations.AddField(
            model_name='room',
            name='geraete',
            field=models.ManyToManyField(to='starsApp.roomdevice'),
        ),
        migrations.AddField(
            model_name='room',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='starsApp.unit'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(blank=True, max_length=3000)),
                ('rate', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('wp', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='starsApp.workplace')),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(14)])),
                ('sonstiges', models.CharField(max_length=160, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wp', models.ManyToManyField(to='starsApp.workplace')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='ProfileUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, null=True, verbose_name='Vorname')),
                ('last_name', models.CharField(max_length=150, null=True, verbose_name='Nachname')),
                ('username', models.CharField(max_length=100, null=True, verbose_name='Benutzername')),
                ('email', models.EmailField(max_length=100, null=True, verbose_name='Email-Adresse')),
                ('avatar', models.ImageField(blank=True, default='anonymous.jpg', null=True, upload_to='')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
