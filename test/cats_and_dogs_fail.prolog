network(CAT).
arc(CAT, 0, 1, "c").
arc(CAT, 1, 2, "a").
arc(CAT, 2, 3, "t").
final(CAT, 3).

network(EMPTY).

network(DOG).
arc(DOG, 0, 1, "d":"c").
arc(DOG, 1, 2, "o":"a").
arc(DOG, 2, 3, "g":"t").
final(DOG, 3, 0.5).

network(CHAT).
arc(CHAT, 0, 1, "c").
arc(CHAT, 1, 2, "a":"h").
arc(CHAT, 2, 3, "t":"a").
arc(CHAT, 3, 4, "0":"t", -1.5).
final(CHAT, 4).

network(FAIL).
arc(FAIL, 0, 1, "foo").
arc(1, 2, "bar").
final(FAIL, 2, 1).

network(CAT).
arc(CAT, 0, 1, "c").
arc(CAT, 1, 2, "a").
arc(CAT, 2, 3, "t").
final(CAT, 3).
