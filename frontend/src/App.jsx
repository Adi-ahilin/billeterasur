import { useState } from "react";
import { registrarUsuario } from "./api";
import "./App.css";

const CAMPOS = [
  { id: "full_name", etiqueta: "Nombre completo", tipo: "text", ejemplo: "Ana Pérez",
    ayuda: "" },
  { id: "rut", etiqueta: "RUT", tipo: "text", ejemplo: "12.345.678-5",
    ayuda: "Con o sin puntos. Se valida el dígito verificador." },
  { id: "email", etiqueta: "Correo electrónico", tipo: "email", ejemplo: "ana@ejemplo.cl",
    ayuda: "" },
  { id: "phone", etiqueta: "Teléfono", tipo: "tel", ejemplo: "+56912345678",
    ayuda: "Formato +56 seguido de 9 dígitos." },
  { id: "password", etiqueta: "Contraseña", tipo: "password", ejemplo: "",
    ayuda: "Mínimo 12 caracteres. No puede ser una clave común ni parecerse a tus datos." },
  { id: "password2", etiqueta: "Repetir contraseña", tipo: "password", ejemplo: "", ayuda: "" },
];

const VACIO = { full_name: "", rut: "", email: "", phone: "", password: "", password2: "" };

export default function App() {
  const [valores, setValores] = useState(VACIO);
  const [errores, setErrores] = useState({});
  const [enviando, setEnviando] = useState(false);
  const [creada, setCreada] = useState(null);

  function cambiar(id, valor) {
    setValores((previos) => ({ ...previos, [id]: valor }));
    if (errores[id]) {
      setErrores((previos) => ({ ...previos, [id]: undefined }));
    }
  }

  async function enviar(evento) {
    evento.preventDefault();
    setEnviando(true);
    setErrores({});

    // La validación del cliente es solo una ayuda visual:
    // el servidor vuelve a validar todo (RS-04).
    const resultado = await registrarUsuario(valores);

    if (resultado.ok) {
      setCreada(resultado.datos);
      setValores(VACIO);
    } else {
      setErrores(resultado.errores);
    }
    setEnviando(false);
  }

  if (creada) {
    return (
      <main className="pantalla">
        <section className="tarjeta exito">
          <div className="marca">BilleteraSur</div>
          <h1>Cuenta creada</h1>
          <p className="mensaje">{creada.mensaje}</p>
          <dl className="resumen">
            <dt>Nombre</dt>
            <dd>{creada.full_name}</dd>
            <dt>Correo</dt>
            <dd>{creada.email}</dd>
            <dt>Identificador</dt>
            <dd className="mono">{creada.id}</dd>
            <dt>Estado</dt>
            <dd>
              <span className="pastilla">
                {creada.is_active ? "Activa" : "Inactiva hasta verificar"}
              </span>
            </dd>
          </dl>
          <p className="pie">
            El identificador es un UUID y no un número correlativo, de modo que no se pueden
            recorrer las cuentas probando valores.
          </p>
          <button className="boton secundario" onClick={() => setCreada(null)}>
            Registrar otra cuenta
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="pantalla">
      <section className="tarjeta">
        <div className="marca">BilleteraSur</div>
        <h1>Crear cuenta</h1>
        <p className="bajada">
          Tu cuenta queda inactiva hasta que verifiques tu correo y tu teléfono.
        </p>

        {errores.general && (
          <div className="alerta" role="alert">
            {errores.general.join(" ")}
          </div>
        )}

        <form onSubmit={enviar} noValidate>
          {CAMPOS.map((campo) => (
            <div className="campo" key={campo.id}>
              <label htmlFor={campo.id}>{campo.etiqueta}</label>
              <input
                id={campo.id}
                name={campo.id}
                type={campo.tipo}
                placeholder={campo.ejemplo}
                value={valores[campo.id]}
                autoComplete={campo.tipo === "password" ? "new-password" : "on"}
                aria-invalid={Boolean(errores[campo.id])}
                aria-describedby={errores[campo.id] ? `${campo.id}-error` : undefined}
                onChange={(evento) => cambiar(campo.id, evento.target.value)}
              />
              {errores[campo.id] ? (
                <p className="error" id={`${campo.id}-error`}>
                  {[].concat(errores[campo.id]).join(" ")}
                </p>
              ) : (
                campo.ayuda && <p className="ayuda">{campo.ayuda}</p>
              )}
            </div>
          ))}

          <button className="boton" type="submit" disabled={enviando}>
            {enviando ? "Creando cuenta…" : "Crear cuenta"}
          </button>
        </form>
      </section>
    </main>
  );
}