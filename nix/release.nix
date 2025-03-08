{ inputs, ... }:

let self = inputs.self;

in {
  flake.overlays.default = final: prev: {
    rsu-taxer-webapp = final.callPackage ./pkgs/webapp.nix {};
    pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
      (python-final: python-prev: {
        rsu-taxer = python-final.callPackage ./pkgs/rsu-taxer.nix {};
      })
    ];
  };

  perSystem = { system, pkgs, ... }: {
    _module.args.pkgs = import inputs.nixpkgs {
      inherit system;
      overlays = [ self.overlays.default ];
    };

    packages = {
      inherit (pkgs) rsu-taxer-webapp;
      inherit (pkgs.python3Packages) rsu-taxer;
    };
  };
}
