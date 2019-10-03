#!/usr/local/bin/bash
IFS=$'\n'

for f in $(find ~/Music -name '*.md'); do
  # Get full filename
  filename=$(basename "$f")
  # Get album from filename
  album="${filename%.*}"
  # Get just the path (no file)
  path_regex="(.*)/.*\.md$"
  [[ $f =~ $path_regex ]] && path="${BASH_REMATCH[1]}"
  # Get the artist from the directory
  artist_regex=".*/(.*)/.*/.*\.md$"
  [[ $f =~ $artist_regex ]] && artist="${BASH_REMATCH[1]}"
  artist_orig="$artist"
  artist=$(echo ${artist,,} | awk '$1=$1' FS=" " OFS="-")
  # Make the required directories
  mkdir -p "./src/music-review/$artist/"
  mkdir -p "./src/_music-review/$artist/"
  mkdir -p "./src/assets/images/music-review/$artist/"
  # Move file into music collection
  cp "$path/$album.md" "./src/_music-review/$artist/$album.md"
  # Get extension of album art picture
  picture_full=$(ls "$path/" | grep "cover")
  picture_ext="${picture_full##*.}"
  # Picture into relevant assets/images subdirectory
  cp "$path/cover.$picture_ext" "./src/assets/images/music-review/$artist/$album.$picture_ext"
  # Create relevant index file
  echo "---" > "./src/music-review/$artist/index.html"
  echo "title: \"$artist_orig\"" >> "./src/music-review/$artist/index.html"
  echo "artist: \"$artist\"" >> "./src/music-review/$artist/index.html"
  cat ./src/scripts/templates/music_index.html >> "./src/music-review/$artist/index.html"
done
