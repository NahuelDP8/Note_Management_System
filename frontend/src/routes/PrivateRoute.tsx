import { Navigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function PrivateRoute({ children }: any) {
  const { token } = useAuth();

  if (!token) {
    return <Navigate to="/" />;
  }

  return children;
}
