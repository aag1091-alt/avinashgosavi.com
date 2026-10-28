  /* Typo helpers for "Did you mean …?", shared by /search/ (search.md) and
     /blog/ (blog.md) — inlined into each page's script, so fix bugs once here.
     typoAdd(vocab, text, weight): count each 3–24 letter word of lowercased text.
     typoClosest(vocab, t): the vocab word within edit distance 1 (2 for words of
     6+ letters; swapped neighbours count as one typo), heavier word wins ties;
     null if none is that close. */
  function typoAdd(vocab, text, weight) {
    (text || '').split(/[^0-9a-zÀ-ɏ]+/).forEach(function(w) {
      if (w.length < 3 || w.length > 24) return;
      vocab[w] = (vocab[w] || 0) + weight;
    });
  }
  function typoDist(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var prev2 = null, prev = [], cur, i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i];
      var low = i;
      for (j = 1; j <= b.length; j++) {
        var c = a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1;
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + c);
        if (prev2 && i > 1 && j > 1 && a.charAt(i - 1) === b.charAt(j - 2) && a.charAt(i - 2) === b.charAt(j - 1))
          cur[j] = Math.min(cur[j], prev2[j - 2] + 1);
        if (cur[j] < low) low = cur[j];
      }
      if (low > max) return max + 1;
      prev2 = prev; prev = cur;
    }
    return prev[b.length];
  }
  function typoClosest(vocab, t) {
    var max = t.length >= 6 ? 2 : 1, best = null, bd = max + 1, bw = 0;
    for (var w in vocab) {
      var d = typoDist(t, w, max);
      if (d < bd || (d === bd && vocab[w] > bw)) { best = w; bd = d; bw = vocab[w]; }
    }
    return bd <= max ? best : null;
  }
