
### Librarii folosite
Am folosit opencv, numpy, os, errno. Din cauza unui bug ciudat in IDE-ul meu, am importat opencv folosind cv2.cv2 in loc de doar cv2, dar nu cred ca ar trebui sa genereze probleme.

### Rularea codului
Dacă folderul de testare o să conțină doar imaginile cu careuri, trebuie doar rulat scriptul main.
Dacă folderul de testare o să conțină și alte fișiere, trebuie comentate liniile 19-23 din Code/IO/load_images.py si schimbate valorile pentru constantele CLASSIC_IMGS și JIGSAW_IMGS la numărul de poze pentru fiecare task. Totuși, cred că acesta este un caz foarte puțin probabil.
De asemenea, codul ar trebuie extras în următorul fel: main.py și folderul Code și templates să fie la același nivel cu folderele de antrenare, testare etc.

### Observatii
Când am început proiectul, nu am observat că deja ne era dat un script de evaluare, așa că mi-am scris și eu propriile funcții. Ele nu mai au nicio utilitate în versiunea actuală a proiectului, dar am decis să le includ, pentru că totuși mi-au fost de mare ajutor pe parcursul proiectului.
Link github: https://github.com/dragosconst/proiect_sudoku. 
