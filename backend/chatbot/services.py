from .client import client
from .prompts import SYSTEM_PROMPT_BASE
from .context import obtener_contexto_proyectos


class ChatbotService:


    def obtener_respuesta(self, mensaje:str, usuario=None):

        try:

            contexto = "Sin información disponible."

            if usuario:
                contexto = obtener_contexto_proyectos(usuario)


            system_prompt = SYSTEM_PROMPT_BASE.format(
                contexto=contexto
            )


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