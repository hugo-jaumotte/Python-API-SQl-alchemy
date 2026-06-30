import { useEffect, useState, useCallback } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { verifyEmail } from "../api/auth.api";

// Once the user is registered, a mail with a vérification link is sent to them
// This function reciver the token from the URL and compare the information with the backend thanks to the route: verifyEmail
// The result is then expressed via the 3 differents useStates below (setLoading, setError, setSucces) 
export default function EmailVerification() {
  const [params] = useSearchParams();
  const navigate = useNavigate();

  const token = params.get("token");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleVerify = useCallback(async () => {
    if (!token) {
      setError(true);
      setLoading(false);
      return;
    }

    try {
      await verifyEmail(token);

      setSuccess(true);

      setTimeout(() => {
        navigate("/", { replace: true });
      }, 300);
    } catch (err) {
      console.error("Error verifying email", err);
      setError(true);
    } finally {
      setLoading(false);
    }
  }, [token, navigate]);

  useEffect(() => {
    handleVerify();
  }, [handleVerify]);

  if (loading) return <h2>Verifying email...</h2>;

  if (error) return <h2 style={{ color: "red" }}>Verification failed</h2>;

  if (success) return <h2 style={{ color: "green" }}>Email verified</h2>;

  return null;
}