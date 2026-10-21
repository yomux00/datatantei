export const SITE_TITLE = "データ探偵ニッポン";
export const SITE_DESCRIPTION =
  "政府統計などの公開データを自分で集計・分析し、「通説は本当か？」を数字で確かめるブログ。分析コードと出典はすべて公開。";
export const REPO_URL = "https://github.com/yomux00/datatantei";

/** base パスを考慮した内部リンク */
export const url = (path = "") =>
  `${import.meta.env.BASE_URL.replace(/\/$/, "")}/${path.replace(/^\//, "")}`;
