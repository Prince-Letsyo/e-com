import ProfileStore from "./profile_store.js";
import ProfileView from "./profile_view.js";

export default function initProfileApp() {
  const profile_view = new ProfileView();
  const profile_store = new ProfileStore();

  profile_store.addEventListener("token_user_backup_code", (_event: Event) => {
    const { dataBackup } = profile_store.store.deviceLinkData;
    if (dataBackup.codes.length <= 3)
    generateBackCodes(profile_view, profile_store);
})
profile_store.addEventListener("token_generate_backup_code", (_event: Event) => {
    const { dataBackup } = profile_store.store.deviceLinkData;
      profile_view.generateBacUpCode(dataBackup);
  });

  profile_store.checkNumberOfBackUpCodes();
}

window.addEventListener("load", initProfileApp);
const generateBackCodes = (view: ProfileView, store: ProfileStore) => {
  view.generateBackCodes("click", (_event: Event) => {
    store.generateTokenBackUp();
  });
};
