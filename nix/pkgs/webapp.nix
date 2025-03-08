{ lib, pnpm_10, stdenv, makeWrapper, nodejs_22 }:

let
  nodejs = nodejs_22;
  pnpm = pnpm_10.override { inherit nodejs; };
in stdenv.mkDerivation (finalAttrs: {
  pname = "analyzer-webapp";
  version = "1.0.0";

  src = ../../webapp;

  nativeBuildInputs = [ nodejs makeWrapper pnpm.configHook ];

  # 获取 pnpm 依赖
  pnpmDeps = pnpm.fetchDeps {
    inherit (finalAttrs) pname version src;
    hash = "sha256-+qC0u1NbwkUdnZyQCIhCBZfh9kGuLHwHyyQzIuK9Y1E=";
  };

  buildPhase = ''
    runHook preBuild

    pnpm install --offline
    pnpm build
    pnpm prune --prod --ignore-scripts

    # 清理缓存和无效软链接
    rm -rf dist/.vite
    find node_modules -xtype l -delete

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall
    mkdir -p $out
    cp -r dist/* $out
    runHook postInstall
  '';

  meta = {
    description = "Analyzer webapp";
    license = lib.licenses.mit;
    platforms = lib.platforms.linux;
  };
})
