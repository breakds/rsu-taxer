{ buildPythonPackage, makeWrapper
, fastapi, uvicorn, numpy, pydantic
, rsu-taxer-webapp }:

buildPythonPackage {
  pname = "rsu-taxer";
  version = "1.0.0";

  srcs = ../../.;

  propagatedBuildInputs = [
    numpy
    fastapi
    uvicorn
    pydantic
  ];

  doCheck = true;

  postInstall = ''
    wrapProgram $out/bin/analyzer \
      --set PNL_FRONTEND ${rsu-taxer-webapp}
  '';
}
