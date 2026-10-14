import type { Plugin } from "@opencode-ai/plugin"

const SIN_CAMBIOS =
  /(already up[ -]?to[ -]?date|ya (est[aá]|ha) actualizado|ja est[aá] atualizado)/i

export const GuiasPostPull: Plugin = async () => {
  return {
    "tool.execute.after": async (input: any, output: any) => {
      try {
        if (!input || input.tool !== "bash") return

        const comando = String(input.args?.command ?? "")
        if (!/\bgit\b[^\n&|;]*\bpull\b/.test(comando)) return

        if (!output || typeof output !== "object") return

        const salida = typeof output.output === "string" ? output.output : ""
        if (SIN_CAMBIOS.test(salida)) return

        const aviso = [
          "",
          "",
          "[[actualizar-guias-post-pull]]",
          "Se ejecutó `git pull` y no figura como \"already up to date\".",
          "Antes de responder al usuario, usa la herramienta skill para cargar y ejecutar `actualizar-guias-post-pull`:",
          "1) inspecciona el diff (`git diff --stat ORIG_HEAD HEAD` y `git log ORIG_HEAD..HEAD --oneline`);",
          "2) decide si los cambios impactan `manual-de-usuario-condosys.md` y/o `MANUAL_TECNICO_CONDOSYS.md`;",
          "3) actualiza solo si hay relación directa, conservando el estilo, o reporta que no hubo impacto.",
        ].join("\n")

        output.output = salida + aviso
      } catch {
        // Nunca interrumpir la ejecución por este aviso.
      }
    },
  }
}
