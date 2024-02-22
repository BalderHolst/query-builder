{
  description = "Nix Flake for sqlite-integrated.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
  };

  outputs = { self , nixpkgs ,... }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
    devDependencies = [
        pkgs.python3Packages.pytest
        pkgs.python3Packages.pdoc
    ];
  in
  {

    # Development shell
    devShells."${system}".default =
    pkgs.mkShell {
        packages = [
            pkgs.python3Packages.pydot
        ] ++ devDependencies;
        shellHook = ''
        make dev
        PYTHONPATH="$(pwd)/build:$PYTHONPATH"
        '';
    };
  };
}
