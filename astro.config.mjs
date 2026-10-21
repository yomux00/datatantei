import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";

// 独自ドメイン取得までは Cloudflare の workers.dev で公開する
export default defineConfig({
  site: "https://datatantei.datatantei.workers.dev",
  trailingSlash: "always",
  integrations: [mdx(), sitemap()],
});
