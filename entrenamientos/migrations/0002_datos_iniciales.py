from django.db import migrations


def crear_datos_iniciales(apps, schema_editor):
    GrupoMuscular = apps.get_model('entrenamientos', 'GrupoMuscular')
    Ejercicio = apps.get_model('entrenamientos', 'Ejercicio')

    grupos = [
        'Pecho',
        'Espalda',
        'Hombros',
        'Bíceps',
        'Tríceps',
        'Piernas',
        'Abdomen',
        'Glúteos',
    ]

    for nombre in grupos:
        GrupoMuscular.objects.get_or_create(nombre=nombre)

    ejercicios = [
        ('Press banca', 'Pecho', 'Ejercicio de pecho con barra.'),
        ('Flexiones', 'Pecho', 'Ejercicio de pecho con peso corporal.'),
        ('Dominadas', 'Espalda', 'Ejercicio de espalda con peso corporal.'),
        ('Remo con barra', 'Espalda', 'Ejercicio de espalda con barra.'),
        ('Sentadilla', 'Piernas', 'Ejercicio principal de piernas.'),
        ('Prensa', 'Piernas', 'Ejercicio de piernas en máquina.'),
        ('Press militar', 'Hombros', 'Ejercicio de hombros con barra.'),
        ('Elevaciones laterales', 'Hombros', 'Ejercicio para hombros con mancuernas.'),
        ('Curl bíceps', 'Bíceps', 'Ejercicio básico para bíceps.'),
        ('Extensión tríceps', 'Tríceps', 'Ejercicio básico para tríceps.'),
        ('Plancha', 'Abdomen', 'Ejercicio isométrico de abdomen.'),
        ('Crunch', 'Abdomen', 'Ejercicio básico de abdomen.'),
        ('Hip thrust', 'Glúteos', 'Ejercicio de glúteos con barra.'),
    ]

    for nombre, grupo, descripcion in ejercicios:
        grupo_muscular = GrupoMuscular.objects.get(nombre=grupo)
        Ejercicio.objects.get_or_create(
            nombre=nombre,
            usuario=None,
            defaults={
                'grupo_muscular': grupo_muscular,
                'descripcion': descripcion,
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('entrenamientos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales),
    ]
