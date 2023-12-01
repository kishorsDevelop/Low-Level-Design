# Design File System using composite design pattern
from abc import ABC, abstractmethod
class FileSystem:
    def add(self, filesystem):
        pass

    def remove(self, filesystem):
        pass
    
    @abstractmethod
    def show(self):
        pass

class File(FileSystem):
    def __init__(self, name):
        self.name = name 

    def show(self):
        print(f"Movie Name : {self.name}")          

class Directory(FileSystem):
    def __init__(self, name):
        self.dir = []
        self.dir_name = name
    
    def add(self, filesystem):
        self.dir.append(filesystem)
    
    def remove(self, filesystem):
        self.dir.remove(filesystem)

    def show(self):
        print(f"{self.dir_name}/")
        for directory in self.dir:
            directory.show()
    
if __name__ == '__main__':
   
   #Creating a marvel movies folder and adding files/movies to it.
   Marvel_Movies = Directory("Marvel Movies")
   iron_man = File("Iron Man")
   Marvel_Movies.add(iron_man)
   Avengers_Movies = Directory("Avengers")
   
   Avengers_movie_1 = File("Avengers: EndGame")
   Avengers_movie_2 = File("Avengers: Infinity War")
   Avengers_movie_3 = File("Avengers: Age of Ultron")
   
   Avengers_Movies.add(Avengers_movie_1)
   Avengers_Movies.add(Avengers_movie_2)
   Avengers_Movies.add(Avengers_movie_3)

   Marvel_Movies.add(Avengers_Movies)

   Marvel_Movies.show()