{ inputs, ... }:

let self = inputs.self;

in {
  perSystem = { system, pkgs, ... }: {
    _module.args.pkgs = import inputs.nixpkgs {
      inherit system;
      overlays = [
        (final: prev: {
          rsu-taxer-webapp = final.callPackage ./pkgs/webapp.nix {};
          pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
            (python-final: python-prev: {
              rsu-taxer = python-final.callPackage ./pkgs/rsu-taxer.nix {};
            })
          ];
        })
      ];
    };

    packages = {
      inherit (pkgs) rsu-taxer-webapp;
      inherit (pkgs.python3Packages) rsu-taxer;
    };
  };
}
