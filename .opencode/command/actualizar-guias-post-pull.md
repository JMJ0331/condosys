---
description: Revisa los cambios del último git pull y actualiza las guías de CONDOSYS solo si impactan su contenido.
agent: build
---

Usa la skill `actualizar-guias-post-pull` (cárgala con la herramienta skill) y aplícala al rango de commits del último `git pull`.

Contexto adicional del usuario (si lo hay): $ARGUMENTS

Pasos obligatorios:
1. Determina el rango con `git diff --stat ORIG_HEAD HEAD` y `git log ORIG_HEAD..HEAD --oneline`. Si sale vacío, usa `HEAD@{1}`.
2. Clasifica los archivos cambiados y decide si impactan `manual-de-usuario-condosys.md` o `MANUAL_TECNICO_CONDOSYS.md`.
3. Si hay impacto, edita esas secciones conservando estilo, tono y estructura. Si no hay impacto, NO modifiques nada.
4. Termina con un reporte breve: rango revisado, archivos con impacto, secciones cambiadas (o "sin cambios").

No hagas commit salvo que el usuario lo pida.
