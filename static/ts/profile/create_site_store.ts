import Store from "../store.js";
import { DataSite } from "../types.js";
import { headers } from "../utils.js";

export default class SiteStore extends Store {
  constructor() {
    super();
  }

  createOrUpdateSiteData(url: string, domain: string, name: string) {
    const { siteData } = this.getState();
    if (siteData.site.name !== name && siteData.site.domain !== domain)
      fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({ name, domain }),
      }).then((data: Response) => {
        if (data.ok)
          data.json().then((dataSite: DataSite) => {
            this.stateHandler(dataSite, "display");
          });
        else data.json().then((e) => console.log(e));
      });
    else this.stateHandler({ domain, name }, "display");
  }

  private stateHandler(dataSite: DataSite, type: string) {
    const cloneState = structuredClone(this.getState());
    cloneState.siteData.site = dataSite;
    cloneState.siteData.type = type;
    this.saveState(cloneState);
  }

  fetchSiteData() {
    fetch(`/auth/site/`).then((data: Response) => {
      if (data.ok)
        data.json().then((dataSite: DataSite) => {
          this.stateHandler(dataSite, "create_update");
        });
      else data.json().then((e) => console.log(e));
    });
  }
}
