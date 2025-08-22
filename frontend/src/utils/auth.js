// Simple auth helper with localStorage
export function saveUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
}

export function getUser() {
  const data = localStorage.getItem("user");
  return data ? JSON.parse(data) : null;
}

export function logout() {
  localStorage.removeItem("user");
}

export function isLoggedIn() {
  return getUser() !== null;
}
