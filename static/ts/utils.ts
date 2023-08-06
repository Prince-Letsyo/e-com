const csrfToken: string | undefined = document?.cookie
  .match("csrftoken")
  ?.input?.split("=")[1];

export const headers: HeadersInit = {
  "Content-Type": "application/json",
  "x-csrftoken": csrfToken!,
};

export const redirect = () => {
    if (window.location.search != "") {
      const redirect_path =
        window.location.search.split("=")[
          window.location.search.split("=").length - 1
        ];
      window.location.href = redirect_path;
    } else window.location.href = "/";
  };
