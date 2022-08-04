from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class ManagerUsuarios(BaseUserManager):
    def create_user(self, nombre_usuario, email, fecha_nacimiento, password=None):
        """
        Crea y guarda un usuario con los parametros de nombre_usuario, email y fecha nacimiento.
        """
        if not nombre_usuario:
            raise ValueError('El usuario debe tener un nombre')

        user = self.model(
            nombre_usuario=nombre_usuario,
            email=self.normalize_email(email),
            fecha_nacimiento=fecha_nacimiento,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, email, fecha_nacimiento, password=None):
        """
    Crea y guarda un super usuario con los mismos parametros. nombre_usuario, email y fecha_nacimiento
        """
        user = self.create_user(
            nombre_usuario=nombre_usuario,
            email=email,
            password=password,
            fecha_nacimiento=fecha_nacimiento,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    nombre_usuario = models.CharField(
        max_length=20,
        verbose_name='Nombre de usuario',
        unique=True
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    fecha_nacimiento = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ManagerUsuarios()

    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['nombre_usuario']

    def __str__(self):
        return self.nombre_usuario

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin