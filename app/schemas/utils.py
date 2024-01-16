from fastapi import Form


def as_form(cls):
    """decorator for you pydantic model to turn them into form models"""
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(
                default=Form(...) if arg.default is arg.empty else Form(arg.default)
            )
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls
