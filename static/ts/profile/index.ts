import ProfileView from "./profile_view.js";

export default function initProfileApp() {
  const profile_view = new ProfileView();
}
window.addEventListener("load", initProfileApp);
