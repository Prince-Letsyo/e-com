export default class View {
  $: Record<string, HTMLInputElement | HTMLSelectElement | Element> = {};
  $$: Record<
    string,
    NodeListOf<Element | HTMLSelectElement | HTMLInputElement>
  > = {};

  constructor() {}

  protected qs(
    selector: string,
    parent?: HTMLInputElement | HTMLSelectElement | Element
  ): HTMLInputElement | HTMLSelectElement | Element {
    const el = parent
      ? parent.querySelector(selector)
      : document.querySelector(selector);
    if (!el) throw new Error("Could not find the element");
    return el;
  }

  protected createElem(tagName: string): HTMLElement {
    return document.createElement(tagName);
  }

  protected qsAll(
    selector: string
  ): NodeListOf<HTMLInputElement | HTMLSelectElement | Element> {
    const elList = document.querySelectorAll(selector);
    if (!elList) throw new Error("Could not find the elements");
    return elList;
  }

  public checkForInputValue(
    elem: HTMLInputElement | HTMLSelectElement | Element
  ) {
    if (elem instanceof HTMLInputElement || elem instanceof HTMLSelectElement) {
      return elem.value;
    }
  }

  protected delegate(
    el: Element,
    selector: string,
    eventKey: string,
    handler: (el: Element) => void
  ) {
    el.addEventListener(eventKey, (event) => {
      if (event.target instanceof Element)
        if (event.target.matches(selector)) {
          handler(event.target);
        }
    });
  }
}
