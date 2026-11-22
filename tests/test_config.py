from app.config import Settings
import pytest

def test_default_settings():
    settings = Settings(_env_file=None)
    
    assert settings.app_env == "development"
    assert settings.app_name == "TaskFlow API"
    assert settings.debug is True
    
    
def test_custom_settings():
    settings = Settings(
        _env_file=None,
        app_env="production",
        app_name="Custom API",
        debug=False
    )

    assert settings.app_env == "production"
    assert settings.app_name == "Custom API"
    assert settings.debug is False
    
def test_environment_variable_priority(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    settings = Settings()
    assert settings.app_env == "production"
    
def test_invalid_debug_value():
    with pytest.raises(ValueError):
        Settings(
            debug = "not a boolean",
            _env_file =None
        )
        