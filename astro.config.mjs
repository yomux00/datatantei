import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";

// 独自ドメイン取得までは GitHub Pages のサブパスで公開する
export default defineConfig({
  site: "https://yomux00.github.io",
  base: "/datatantei",
  trailingSlash: "always",
  integrations: [mdx(), sitemap()],
});
