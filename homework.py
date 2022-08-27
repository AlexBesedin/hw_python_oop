from dataclasses import dataclass, asdict
from typing import Sequence, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message_template = ('Тип тренировки: {training_type}; '
                        'Длительность: {duration:.3f} ч.; '
                        'Дистанция: {distance:.3f} км; '
                        'Ср. скорость: {speed:.3f} км/ч; '
                        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message_template.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Длина шага
    M_IN_KM: int = 1000  # Коэффициент для перевода метра в километры
    MIN_IN_HOUR: int = 60  # Коэффициент для перевода минуты в часы

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Необходимо определить get_spent_calories")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    MEAN_SPEED_MULTIPLE: int = 18  # Первый коэффициент
    MEAN_SPEED_SUBTRAHEND: int = 20  # Второй коэффициент

    def get_spent_calories(self) -> float:
        multiple_and_speed = self.MEAN_SPEED_MULTIPLE * self.get_mean_speed()
        cal = multiple_and_speed - self.MEAN_SPEED_SUBTRAHEND
        duration_and_min_in_hour = self.duration * self.MIN_IN_HOUR
        calories = cal * self.weight / self.M_IN_KM * duration_and_min_in_hour
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_WALK_1: float = 0.035  # Первый коэффициент
    COEFF_WALK_2: float = 0.029  # Второй коэффициент

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        duration_in_min = self.duration * self.MIN_IN_HOUR
        coeff_and_weight_1 = self.COEFF_WALK_1 * self.weight
        coeff_and_weight_2 = speed ** 2 // self.height
        coeff_walk_2_and_weight = self.COEFF_WALK_2 * self.weight
        mean_speed_and_weight = coeff_and_weight_2 * coeff_walk_2_and_weight
        return (coeff_and_weight_1 + mean_speed_and_weight) * duration_in_min


class Swimming(Training):
    """Тренировка: плавание."""
    SWM_COEFF_1: float = 1.1
    SWM_COEFF_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories_1 = self.get_mean_speed() + self.SWM_COEFF_1
        calories = calories_1 * self.SWM_COEFF_2 * self.weight
        return calories


def read_package(workout_type: str, data: Sequence[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    trainings = Dict[str, Type[Training]]

    trainings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in trainings:
        raise NotImplementedError('Данный вид тренировки отсутствует')

    return trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
