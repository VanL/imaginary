

from zope.interface import Interface, implements, directlyProvides
from zope.interface.verify import verifyObject

from twisted.trial import unittest

from axiom import store, item, attributes

from imaginary.test import commandutils
from imaginary import iimaginary, plugins, creation
from imaginary.creation import createCreator
from imaginary.plugins import imaginary_basic



class ThingPlugin(commandutils.CommandTestCaseMixin, unittest.TestCase):
    """
    Tests for L{imaginary_basic.thingPlugin}, a plugin for creating simple
    things with no special behavior.
    """
    def test_createThing(self):
        """
        L{plugins.thingPlugin} creates a L{Thing} with no additional behavior.
        """
        st = store.Store()
        thing = imaginary_basic.thingPlugin.getType()(store=st, name=u"foo")
        self.assertTrue(verifyObject(iimaginary.IThing, thing))
        self.assertIdentical(thing.store, st)
        self.assertEqual(thing.name, u"foo")


    def test_createThingCommand(self):
        """
        Things can be created with the I{create} command.
        """
        self._test(
            "create thing foo",
            ["Foo created."],
            ["Test Player creates foo."])
        [foo] = self.playerContainer.getContents()
        self.assertEqual(foo.name, u"foo")



class IFoo(Interface):
    pass



class Foo(item.Item):
    implements(IFoo)
    powerupInterfaces = (IFoo,)

    foo = attributes.text()



createFoo = createCreator((Foo, {'foo': u'bar'}))



class FooPlugin(object):
    directlyProvides(iimaginary.IThingType)

    type = 'foo'

    def getType(cls):
        return createFoo
    getType = classmethod(getType)



class CreateTest(commandutils.CommandTestCaseMixin, unittest.TestCase):
    def _getPlugins(self, iface, package):
        self.assertIdentical(iface, iimaginary.IThingType)
        self.assertIdentical(package, plugins)
        return [FooPlugin]


    def setUp(self):
        self.old_getPlugins = creation.getPlugins
        creation.getPlugins = self._getPlugins
        return commandutils.CommandTestCaseMixin.setUp(self)


    def tearDown(self):
        creation.getPlugins = self.old_getPlugins
        return commandutils.CommandTestCaseMixin.tearDown(self)


    def testCreate(self):
        self._test(
            "create foo bar",
            ["Bar created."],
            ["Test Player creates bar."])
        foobar = self.find(u"bar")
        self.assertEquals(foobar.name, "bar")
        self.assertEquals(foobar.description, "an undescribed object")
        self.assertEquals(foobar.location, self.player)
        foo = IFoo(foobar)
        self.failUnless(isinstance(foo, Foo))
        self.assertEquals(foo.foo, u"bar")

        self._test(
            "create foo 'bar foo'",
            ["Bar foo created."],
            ["Test Player creates bar foo."])
        barfoo = self.find(u"bar foo")
        self.assertEquals(barfoo.name, "bar foo")
        self.assertEquals(barfoo.description, 'an undescribed object')
        self.assertEquals(barfoo.location, self.player)

        self._test(
            "create foo 'described thing' This is the things description.",
            ["Described thing created."],
            ["Test Player creates described thing."])
        thing = self.find(u"described thing")
        self.assertEquals(thing.name, "described thing")
        self.assertEquals(thing.description, "This is the things description.")
        self.assertEquals(thing.location, self.player)
