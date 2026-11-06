import { Navigate, Link, useNavigate } from "react-router-dom";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { loginApi } from "../../api/user";
import { useAuth } from "../../hooks/useAuth";

export function Login() {
  const { auth, login } = useAuth();
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: initialValues(),
    validationSchema: validationSchema(),
    validateOnChange: false,
    onSubmit: async (formValues) => {
      try {
        const response = await loginApi(formValues);
        const { access } = response;
        // Evidencia solicitada: el token obtenido se muestra en la consola (solo en desarrollo)
        if (import.meta.env.DEV) console.log("Token JWT obtenido:", access);
        await login(access); // guarda el token y carga los datos del usuario
        navigate("/dashboard");
      } catch (error) {
        toast.error(error.message);
      }
    },
  });

  // Si ya hay sesión no tiene sentido mostrar el formulario
  if (auth) return <Navigate to="/dashboard" replace />;

  return (
    <div className="login-admin">
      <div className="login-admin__content">
        <h1>Login</h1>
        <Form className="login-form-admin" onSubmit={formik.handleSubmit}>
          <label>Correo electrónico</label>
          <Form.Input
            name="email"
            placeholder="Correo electrónico"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.errors.email}
          />
          <label>Contraseña</label>
          <Form.Input
            name="password"
            type="password"
            placeholder="Contraseña"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.errors.password}
            autoComplete="current-password"
          />
          <Button type="submit" content="Iniciar Sesión" primary fluid loading={formik.isSubmitting} />
        </Form>
        <div className="login-admin__links">
          ¿No tienes cuenta? <Link to="/register">Regístrate</Link>
        </div>
      </div>
    </div>
  );
}

function initialValues() {
  return { email: "", password: "" };
}

function validationSchema() {
  return Yup.object({
    email: Yup.string()
      .email("Correo electrónico no válido")
      .required("El correo electrónico es obligatorio"),
    password: Yup.string().required("La contraseña es obligatoria"),
  });
}
