
### Librarii folosite
Am folosit opencv, numpy, os, errno. Din cauza unui bug ciudat in IDE-ul meu, am importat opencv folosind cv2.cv2 in loc de doar cv2, dar nu cred ca ar trebui sa genereze probleme.
Versiuni librarii:
numpy = 1.19.5
opencv = 4.5.3


### Rularea codului
Dacă folderul de testare o să conțină doar imaginile cu careuri, trebuie doar rulat scriptul main.py, va rezolva ambele task-uri si bonusul lor.
Dacă folderul de testare o să conțină și alte fișiere, trebuie comentate liniile 19-23 din Code/IO/load_images.py si schimbate valorile pentru constantele CLASSIC_IMGS și JIGSAW_IMGS la numărul de poze pentru fiecare task. Totuși, cred că acesta este un caz foarte puțin probabil, doar nu sunt foarte sigur dacă am înțeles care o să fie formatul folderului de testare.
De asemenea, codul ar trebuie extras din arhivă în următorul fel: main.py și folderul Code și templates să fie la același nivel cu folderele de antrenare, testare etc. Este posibil ca numpy să afișeze niște warning-uri pentru că am folosit un constructor deprecated pentru np.array, dar nu ridică probleme la runtime.

### Observatii
Când am început proiectul, nu am observat că deja ne era dat un script de evaluare, așa că mi-am scris și eu propriile funcții. Ele nu mai au nicio utilitate în versiunea actuală a proiectului, dar am decis să le includ, pentru că totuși mi-au fost de mare ajutor pe parcursul proiectului.
Link github: https://github.com/dragosconst/proiect_sudoku. 
