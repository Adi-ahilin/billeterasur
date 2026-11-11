const BASE = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api/v1";

/**
 * Registra una cuenta nueva.
 * Devuelve { ok: true, datos } o { ok: false, errores }.
 * Los errores vienen del servidor por campo: { rut: ["..."], email: ["..."] }.
 */
export async function registrarUsuario(datos) {
  let respuesta;
  try {
    respuesta = await fetch(`${BASE}/registro/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });
  } catch {
    return {
      ok: false,
      errores: { general: ["No se pudo conectar con el servidor. ¿Está corriendo la API?"] },
    };
  }

  if (respuesta.status === 201) {
    return { ok: true, datos: await respuesta.json() };
  }

  if (respuesta.status === 429) {
    return {
      ok: false,
      errores: { general: ["Demasiados intentos de registro. Espera unos minutos."] },
    };
  }

  let cuerpo = {};
  try {
    cuerpo = await respuesta.json();
  } catch {
    cuerpo = { general: ["El servidor respondió de forma inesperada."] };
  }
  return { ok: false, errores: cuerpo };
}