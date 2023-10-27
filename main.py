
str_country = 'Россия:17 234 035:1000000' \
              '|Антарктида:14 107 000' \
              '|Канада:9 984 670:203423'


class RawStrValidator:
    def __init__(self, raw_str):
        if not raw_str:
            raise ValueError('Сырая строка не может быть пустой')

        if self.DELIMITER not in raw_str:
            raise ValueError(
                f'Строка должна содержать разделитель '
                f'"{self.DELIMITER}"'
            )


class Country(RawStrValidator):
    DELIMITER = ':'

    def __init__(self, raw_str):
        super().__init__(raw_str)
        temp_raw_data = raw_str.split(self.DELIMITER)

        self.name = temp_raw_data[0]
        self.square = int(temp_raw_data[1].replace(' ', ''))
        self.population = (
            int(temp_raw_data[2].replace(' ', ''))
            if len(temp_raw_data) > 2 else 0
        )

    @property
    def is_empty(self):
        return not bool(self.name)

    @property
    def info(self):
        return f'{self.name} ' \
               f'(Площадь: {self.square} км2) ' \
               f'[Численность: {self.population}]'


class Countries(RawStrValidator):
    DELIMITER = '|'

    def _init_(self, raw_str):
        super()._init_(raw_str)
        self.__data = []
        self._prepare_raw_str(raw_str)

    def _prepare_raw_str(self, raw_str):
        for country_str in raw_str.split(self.DELIMITER):
            country = Country(country_str)

            if not country.is_empty:
                self.__data.append(country)

    def get(self, index):
        max_index = len(self.__data) - 1
        if index > max_index:
            raise ValueError(
                f'Нет страны с индексом {index}. '
                f'Максимальный индекс - {max_index}'
            )

        print(self.__data[index].info)

    def find(self, search_str):
        if not search_str:
            raise ValueError('Поискова строка не может быть пустой')

        for item in self.__data:
            if search_str in item.name:
                print(item.info)

    def get_more_square(self, square):
        self._compare(square, 'square')

    def get_less_square(self, square):
        self._compare(square, 'square', False)

    def get_more_population(self, population):
        self._compare(population, 'population')

    def get_less_population(self, population):
        self._compare(population, 'population', False)

    def _compare(self, value, field_name, more=True):
        for item in self.__data:
            if (
                    (value < getattr(item, field_name)) if more
                    else (value > getattr(item, field_name))
            ):
                print(item.info)


countries = Countries(str_country)
countries.get(0) # Получить страну из списка по индексу
countries.find('Анта') # Поиск стран по слову
countries.get_more_square(100000) # Страны с площадью больше
countries.get_less_square(100000) # Страны с площадью меньше
countries.get_more_population(100000) # Страны с населением больше
countries.get_less_population(100000) # Страны с населением меньше
