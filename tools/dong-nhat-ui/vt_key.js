function vtKey(h){h=h.replace(/\s+/g,' ').trim();
  if(h==='#')return 'n';if(h==='词'||h==='词语'||h==='Chữ Hán'||h==='Từ vựng')return 'w';if(h==='Pinyin')return 'p';
  if(h==='词性'||h==='Loại từ'||h==='Từ loại')return 't';if(h==='Hán Việt'||h==='Hán-Việt')return 'hv';
  if(/^Nghĩa( tiếng Việt)?/.test(h))return 'm';if(h==='English')return 'e';
  if(h==='例句'||h==='Giải thích'||/^Ghi chú/.test(h)||/^Ví dụ/.test(h))return 'x';return null}
