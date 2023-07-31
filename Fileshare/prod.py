import environ
import os


env = environ.Env()
environ.Env.read_env()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': env("HOST"),
        'NAME': env("NAME"),
        'USER': env("USER"),
        'PASSWORD':env("PASSWORD"),
        'PORT':env("PORT"),

    }
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME':env('CLOUD_NAME'),
    'API_KEY':env('API_KEY'),
    'API_SECRET':env('API_SECRET'), 
}

STORAGES = {'default':{"BACKEND":'cloudinary_storage.storage.MediaCloudinaryStorage'
}, 
"staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }, 
} 