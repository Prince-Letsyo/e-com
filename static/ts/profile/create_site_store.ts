import Store from "../store.js";
import { DataSite, DataSiteError, MainStore } from "../types.js";
import { headers } from "../utils.js";

export default class SiteStore extends Store {
  constructor() {
    super();
  }

  createOrUpdateSiteData(url: string, domain: string, name: string) {
    const { siteData } = this.getState();
    if (siteData.site.name !== name || siteData.site.domain !== domain)
      fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({ name, domain }),
      }).then((data: Response) => {
        if (data.ok)
          data.json().then((dataSite: DataSite) => {
            this.stateHandler(dataSite);
            this.dispatchType("site_display");
          });
        else
          data.json().then((error:DataSiteError) => {
            this.saveState((prevState: MainStore) => {
              prevState.siteData.errors = error;
              return prevState;
            });
            this.dispatchType("site_display_error");
          });
      });
    else {
      this.stateHandler({ domain, name });
      this.dispatchType("site_display");
    }
  }

  private stateHandler(dataSite: DataSite) {
    this.saveState((prevState: MainStore) => {
      prevState.siteData.site = dataSite;
      return prevState;
    });
  }

  fetchSiteData() {
    fetch(`/auth/site/`).then((data: Response) => {
      if (data.ok)
        data.json().then((dataSite: DataSite) => {
          this.stateHandler(dataSite);
          this.dispatchType("site_create_update");
        });
      else data.json().then((e) => console.log(e));
    });
  }
}
