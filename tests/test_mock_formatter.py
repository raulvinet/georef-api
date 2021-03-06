from unittest import TestCase
from service import formatter


class FormattingTest(TestCase):
    def test_fields_list_to_dict(self):
        """El resultado de fields_list_to_dict debería ser un diccionario
        equivalente a los valores de una lista, desaplanados."""
        fields = [
            'id',
            'nombre',
            'provincia.id',
            'provincia.nombre',
            'ubicacion.lat',
            'ubicacion.lon',
            'prueba.foo.bar',
            'prueba.foo.baz'
        ]

        fields_dict = formatter.fields_list_to_dict(fields)
        self.assertEqual(fields_dict, {
            'id': True,
            'nombre': True,
            'provincia': {
                'id': True,
                'nombre': True
            },
            'ubicacion': {
                'lat': True,
                'lon': True
            },
            'prueba': {
                'foo': {
                    'bar': True,
                    'baz': True
                }
            }
        })

    def test_flatten_dict(self):
        """Se debería aplanar un diccionario correctamente."""
        original = {
            'provincia': {
                'id': '06',
                'nombre': 'BUENOS AIRES'
            },
            'foo': 'bar'
        }

        formatter.flatten_dict(original)
        self.assertEqual(original, {
            'provincia_id': '06',
            'provincia_nombre': 'BUENOS AIRES',
            'foo': 'bar'
        })

    def test_filter_result_fields(self):
        """Se debería poder filtrar los campos de un diccionario, utilizando
        otro diccionario para especificar cuáles campos deberían ser
        mantenidos."""
        result = {
            'simple': 'foo',
            'removed': 'foo',
            'nested': {
                'field1': 'foo',
                'field2': 'foo',
                'removed': 'foo',
                'nested2': {
                    'field1': 'foo',
                    'removed': 'foo'
                }
            }
        }

        fields = [
            'simple',
            'nested.field1',
            'nested.field2',
            'nested.nested2.field1'
        ]

        formatter.filter_result_fields(result,
                                       formatter.fields_list_to_dict(fields))
        self.assertEqual(result, {
            'simple': 'foo',
            'nested': {
                'field1': 'foo',
                'field2': 'foo',
                'nested2': {
                    'field1': 'foo'
                }
            }
        })
