const nativeFetch = window.fetch.bind(window);

window.fetch = (input: RequestInfo | URL, init?: RequestInit) => {
  const url = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
  if (
    /rex-api-call|immobilien-experten\.de|ee-experten\.com|bafa\.ee-experten|googletagmanager|google-analytics|facebook|doubleclick|hotjar/.test(
      url,
    )
  ) {
    return Promise.resolve(new Response("", { status: 204 }));
  }
  return nativeFetch(input, init);
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('[class*="referencesSwiper"]').forEach((swiper) => {
    const block = swiper.closest(".py-0.bg-white") ?? swiper.parentElement;
    block?.remove();
  });
});

document.addEventListener(
  "submit",
  (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    if (form.id === "iwf-form") {
      event.preventDefault();
    }
  },
  true,
);
