#!/usr/bin/python3
"""This module defines the console for the AirBnB clone project"""
import cmd
import shlex
from models.engine.db_storage import DBStorage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """Defines the behavior of the command interpreter"""
    prompt = '(hbnb) '

    def do_create(self, arg):
        """Creates a new instance of a class"""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        if not arg:
            print("** class name missing **")
            return
        args = shlex.split(arg)
        if args[0] not in storage.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        args = shlex.split(arg)
        if args[0] not in storage.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        storage.all().pop(key)
        storage.save()

    def do_all(self, arg):
        """Prints all string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if not arg:
            obj_list = list(storage.all().values())
        elif args[0] in storage.classes:
            obj_list = [obj for obj in storage.all().values()
                        if type(obj).__name__ == args[0]]
        else:
            print("** class doesn't exist **")
            return
        print([str(obj) for obj in obj_list])

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
            return
        args = shlex.split(arg)
        if args[0] not in storage.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        setattr(storage.all()[key], args[2], args[3])
        storage.all()[key].save()

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        count = 0
        args = shlex.split(arg)
        if args[0] in storage.classes:
            count = sum(1 for obj in storage.all().values()
                        if type(obj).__name__ == args[0])
        else:
            print("** class doesn't exist **")
            return
        print(count)

    def do_quit(self, arg):
        """Exits the command interpreter"""
        return True

    def do_EOF(self, arg):
        """Handles the EOF signal"""
        print()
        return True

    def emptyline(self):
        """Handles empty lines"""
        pass


if __name__ == '__main__':
    storage = DBStorage()
    storage.reload()
    HBNBCommand().cmdloop()

