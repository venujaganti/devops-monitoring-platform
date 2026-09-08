export function isRequired(value) {
  return (
    value !== null &&
    value !== undefined &&
    String(value).trim().length > 0
  );
}

export function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function isValidPassword(password) {
  return typeof password === "string" && password.length >= 8;
}

export function validateLogin(username, password) {
  const errors = {};

  if (!isRequired(username)) {
    errors.username = "Username is required";
  }

  if (!isRequired(password)) {
    errors.password = "Password is required";
  }

  return errors;
}