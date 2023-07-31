# Web Preview

## Install dependencies

```powershell
cd ./web
npm install
```

## Running tailwindcss

```powershell
npx tailwindcss -i ./web/css/input.css -o ./web/css/output.css --watch
```

## Updating the github pages

There is a github action that will trigger on changes of this folder, it will push some files to the `gh-pages` branch.
