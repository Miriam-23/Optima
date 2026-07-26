from .client import client
from .prompts import SYSTEM_PROMPT_BASE
from .context import obtener_contexto_equipo, obtener_contexto_proyectos, obtener_contexto_tareas, obtener_contexto_dashboard


class ChatbotService:


    def obtener_respuesta(self, mensaje:str, usuario=None):

        try:

            contexto = "Sin información disponible."

            if usuario:
                contexto_proyectos  = obtener_contexto_proyectos(usuario)
                contexto_tareas = obtener_contexto_tareas(usuario)
                contexto_equipo = obtener_contexto_equipo(usuario)
                contexto_dashboard = obtener_contexto_dashboard(usuario)

                contexto = (
                    f"{contexto_proyectos}\n\n"
                    f"{contexto_tareas}\n\n"
                    f"{contexto_equipo}\n\n"
                    f"{contexto_dashboard}"
                )

            system_prompt = SYSTEM_PROMPT_BASE.format(
                contexto=contexto
            )

            # print(contexto)

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",

                messages=[
                    {
                        "role":"system",
                        "content":system_prompt
                    },
                    {
                        "role":"user",
                        "content":mensaje
                    }
                ],

                max_tokens=1024,
                temperature=0.7
            )


            return completion.choices[0].message.content


        except Exception as e:

            print(f"Error al conectar con Groq: {e}")

            return (
                "En este momento el asistente no está disponible. "
                "Por favor intenta nuevamente."
            )