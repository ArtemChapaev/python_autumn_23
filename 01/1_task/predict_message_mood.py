class SomeModel:
    def predict(self, message: str) -> float:
        if not isinstance(message, str):
            raise TypeError("message must be str")

        if len(message) > 10:
            return len(message) % 2
        return len(message) / 10


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    if not isinstance(message, str):
        raise TypeError("message must be str")
    if not isinstance(model, SomeModel):
        raise TypeError("model must be SomeModel")

    if not isinstance(bad_thresholds, float) and not isinstance(bad_thresholds, int):
        raise TypeError("thresholds must be float")
    if not isinstance(good_thresholds, float) and not isinstance(good_thresholds, int):
        raise TypeError("thresholds must be float")

    if not 0.0 <= bad_thresholds <= 1.0 or not 0.0 <= good_thresholds <= 1.0:
        raise ValueError("thresholds must be bigger than 0.0 and less than 1.0")
    if bad_thresholds > good_thresholds:
        raise ValueError("good_thresholds must be bigger than bad_thresholds")

    pred = model.predict(message)
    if pred < bad_thresholds:
        return "неуд"
    if pred > good_thresholds:
        return "отл"
    return "норм"
