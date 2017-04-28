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
  # mkdir -p "./music/$artist/$album"
  # mkdir -p "./assets/images/music/$artist/$album"

  # if [[ $f =~ $regex ]]
  # then
  #   artist="${BASH_REMATCH[1]}"
  #   echo "$artist"
  # else
  #   echo "no match"
  # fi
  # artist=$(exiftool -AlbumArtist "$f" | cut -d ':' -f 2)
  # # If no album artist is identified, use the artist
  # # NOTE: This is a bad idea and will probably lead to 
  # #   unintended sorting behavior
  # if [[ -z "${param// }" ]]; then
  # 	artist=$(exiftool -Artist "$f" | cut -d ':' -f 2)
  # fi
  # album=$(exiftool -Album "$f" | cut -d ':' -f 2)
  # title=$(exiftool -Title "$f" | cut -d ':' -f 2)
  # tracknumber=$(exiftool -Tracknumber "$f" | cut -d ':' -f 2)
  # # Nuke leading spaces
  # artist=${artist#" "}
  # album=${album#" "}
  # title=${title#" "}
  # tracknumber=${tracknumber#" "}
  # if [ $# == 1 ]; then
  #   case $1 in
  #     --test)
  #       echo "$artist/$album/$filename.$extension"
  #       #echo "$artist/$album/$tracknumber $title.$extension"
  #     ;;
  #     *)
  #       echo "Invalid argument."
  #     ;;
  #   esac
  # else
  #   if [ ! -d "$DIR/$artist" ]; then
  #     #echo "What the fuck: $DIR/$artist"
  #     mkdir "$DIR/$artist/"
  #   fi
  #   if [ ! -d "$DIR/$artist/$album" ]; then
  #     # echo "What the fuck: $DIR/$artist/$album"
  #     mkdir "$DIR/$artist/$album/"
  #   fi
  #   mv -f "$f" "$DIR/$artist/$album/$filename.$extension"
  # fi
done

echo "Done!"
