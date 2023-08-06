import SiteStore from "./create_site_store.js";
import SiteView from "./create_site_view.js";

export default function initSiteApp() {
  const site_view = new SiteView();
  const site_store = new SiteStore();
  site_store.addEventListener("statechange", (event: Event) => {
    const {type, site} = site_store.store.siteData
    if (type === "create_update") {
      site_view.reCreateSite(site);
      site_view.createSite();
      createSite(site_view, site_store, site_view.update_url);
    } else {
      site_view.displaySite(site);
      eidiSite(site_view, site_store);
    }
  });

  createSite(site_view, site_store, site_view.create_url);
  eidiSite(site_view, site_store);
}

window.addEventListener("load", initSiteApp);

const eidiSite = (view: SiteView, store: SiteStore) => {
  view.editSubmitedSite("click", (event: Event) => {
    event.preventDefault();
    store.fetchSiteData();
  });
};

const createSite = (view: SiteView, store: SiteStore, url: string) => {
  view.submitSite("click", (event: Event) => {
    event.preventDefault();

    const domain: string | undefined = view.checkForInputValue(
      view.$.domainName
    ) as string;
    const name: string | undefined = view.checkForInputValue(
      view.$.displayName
    ) as string;
    store.createOrUpdateSiteData(url, domain, name);
  });
};
