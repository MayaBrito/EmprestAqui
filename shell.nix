let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.flask
      python-pkgs.flask-wtf
      python-pkgs.faker
      python-pkgs.nltk
    ]))
  ];
}
