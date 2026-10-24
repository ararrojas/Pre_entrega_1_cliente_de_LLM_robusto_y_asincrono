"""Cadena LCEL asíncrona: ChatPromptTemplate | modelo | StrOutputParser."""
import asyncio
import os
import sys

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Sos un asistente técnico. Respondé en 3 líneas como máximo."),
        ("human", "{pregunta}"),
    ]
)

# claude-sonnet-5-5 no admite temperature distinta de la default, por eso no se fija
model = ChatAnthropic(model_name="claude-sonnet-5-5", max_tokens=1024)

chain = prompt | model | StrOutputParser()


async def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("Falta ANTHROPIC_API_KEY: copiá .env.example a .env y completalo.")
    try:
        respuesta = await chain.ainvoke({"pregunta": "¿Qué es la entropía?"})
    except Exception as exc:
        sys.exit(f"Error al invocar la cadena: {type(exc).__name__}: {exc}")
    print(respuesta)


if __name__ == "__main__":
    asyncio.run(main())
