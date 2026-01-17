# Instrucciones para subir a GitHub

El proyecto está listo para ser subido a GitHub. Sigue estos pasos:

## 1. Crear el repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `api-docs-normalizer`
3. Descripción: "Transforma documentación de APIs desordenada en esquemas OpenAPI 3.0 listos para producción"
4. Elige si será público o privado
5. **NO** inicialices con README, .gitignore o licencia (ya los tenemos)
6. Clic en "Create repository"

## 2. Conectar el repositorio local con GitHub

Ejecuta estos comandos (reemplaza `TU_USUARIO` con tu usuario de GitHub):

```bash
cd /Users/luisruizdearbulo/Desktop/api-docs-normalizer

# Agregar el remote
git remote add origin https://github.com/TU_USUARIO/api-docs-normalizer.git

# O si prefieres SSH:
# git remote add origin git@github.com:TU_USUARIO/api-docs-normalizer.git

# Verificar que está configurado
git remote -v

# Subir el código
git branch -M main
git push -u origin main
```

## 3. Verificar

Una vez subido, verifica que:
- El README se muestra correctamente
- Los archivos están todos presentes
- El LICENSE está visible

## Notas adicionales

- El proyecto ya tiene un commit inicial con todo el código
- El `.gitignore` está configurado correctamente
- El README incluye badges que funcionarán una vez esté en GitHub
